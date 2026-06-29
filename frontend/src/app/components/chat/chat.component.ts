import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked, signal } from '@angular/core';
import { NgClass, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DocumentService } from '../../services/document.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [NgClass, FormsModule, DatePipe],
  templateUrl: './chat.html',
  styleUrls: ['./chat.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  docId = signal(0);
  documentName = signal('');
  question = signal('');
  loading = signal(false);
  messages = signal<any[]>([]);
  private shouldScroll = false;

  constructor(
    private docService: DocumentService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.docId.set(+params['id']);
      if (this.docId()) {
        this.loadDocument();
      } else {
        this.router.navigate(['/documents']);
      }
    });
  }

  ngAfterViewChecked() {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  async loadDocument() {
    try {
      const response = await this.docService.getDocument(this.docId());
      this.documentName.set(response.data.original_filename);
    } catch {
      alert('Failed to load document');
      this.router.navigate(['/documents']);
    }
  }

  async askQuestion() {
    const q = this.question().trim();
    if (!q) return;

    this.messages.update(msgs => [...msgs, { role: 'user', content: q, timestamp: new Date() }]);
    this.question.set('');
    this.loading.set(true);
    this.shouldScroll = true;

    try {
      const response = await this.docService.askQuestion(this.docId(), q);
      this.messages.update(msgs => [...msgs, { role: 'assistant', content: response.data.answer, timestamp: new Date() }]);
    } catch (error: unknown) {
      const msg = error as { response?: { data?: { detail?: string } }; message?: string };
      this.messages.update(msgs => [...msgs, {
        role: 'error',
        content: '❌ Failed to get answer: ' + (msg.response?.data?.detail || msg.message),
        timestamp: new Date()
      }]);
    } finally {
      this.loading.set(false);
      this.shouldScroll = true;
    }
  }

  scrollToBottom() {
    try {
      this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
    } catch { /* ignore */ }
  }

  clearChat() {
    this.messages.set([]);
  }

  goBack() {
    this.router.navigate(['/documents']);
  }
}
