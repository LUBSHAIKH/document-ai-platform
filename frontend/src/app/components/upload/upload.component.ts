import { Component, signal } from '@angular/core';
import { NgClass } from '@angular/common';
import { DocumentService } from '../../services/document.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [NgClass],
  templateUrl: './upload.html',
  styleUrls: ['./upload.css']
})
export class UploadComponent {
  selectedFile = signal<File | null>(null);
  uploadMessage = signal('');
  isLoading = signal(false);

  constructor(private docService: DocumentService) {}

  onFileSelected(event: Event) {
    const files = (event.target as HTMLInputElement).files;
    if (files && files.length > 0) {
      this.selectedFile.set(files[0]);
      this.uploadMessage.set('');
    }
  }

  async uploadFile() {
    const file = this.selectedFile();
    if (!file) {
      this.uploadMessage.set('⚠️ Please select a file');
      return;
    }

    this.isLoading.set(true);
    this.uploadMessage.set('');

    try {
      const response = await this.docService.uploadDocument(file);
      this.uploadMessage.set(`✅ Uploaded: ${response.data.original_filename}`);
      this.selectedFile.set(null);

      const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
      if (fileInput) fileInput.value = '';

      setTimeout(() => this.uploadMessage.set(''), 3000);
    } catch (error: any) {
      this.uploadMessage.set(`❌ Upload failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      this.isLoading.set(false);
    }
  }
}
