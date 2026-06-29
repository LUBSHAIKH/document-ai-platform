import { Component, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { NgClass } from '@angular/common';
import { DocumentService } from '../../services/document.service';

@Component({
  selector: 'app-documents',
  templateUrl: './documents.html',
  styleUrls: ['./documents.css'],
  standalone: true,
  imports: [NgClass, RouterLink],
})
export class DocumentsComponent implements OnInit {
  documents = signal<any[]>([]);
  isLoading = signal(true);
  errorMessage = signal('');
  indexingIds = signal<Set<number>>(new Set());

  constructor(private docService: DocumentService, private router: Router) {}

  ngOnInit() {
    this.loadDocuments();
  }

  loadDocuments() {
    this.isLoading.set(true);
    this.errorMessage.set('');
    this.docService.getDocuments()
      .then((response: any) => {
        this.documents.set(response.data.documents ?? []);
      })
      .catch(() => {
        this.errorMessage.set('Failed to load documents');
      })
      .finally(() => {
        this.isLoading.set(false);
      });
  }

  indexDocument(id: number) {
    this.indexingIds.update(s => new Set([...s, id]));
    this.docService.indexDocument(id)
      .then(() => {
        alert('✅ Document indexed successfully!');
        this.documents.update(docs =>
          docs.map(d => d.id === id ? { ...d, indexed: true } : d)
        );
      })
      .catch(() => {
        alert('❌ Failed to index');
      })
      .finally(() => {
        this.indexingIds.update(s => { const next = new Set(s); next.delete(id); return next; });
      });
  }

  selectDocument(doc: any) {
    if (!doc.indexed) {
      alert('Please index first!');
      return;
    }
    this.router.navigate(['/chat', doc.id]);
  }

  deleteDocument(id: number) {
    if (!confirm('Delete?')) return;
    this.docService.deleteDocument(id)
      .then(() => this.loadDocuments())
      .catch(() => alert('Delete failed'));
  }

  getFormattedDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}
