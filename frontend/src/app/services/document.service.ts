import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = 'http://localhost:8000/api/documents';

  constructor() {}

  uploadDocument(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${this.apiUrl}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  getDocuments() {
    return axios.get(this.apiUrl);
  }

  getDocument(id: number) {
    return axios.get(`${this.apiUrl}/${id}`);
  }

  indexDocument(id: number) {
    return axios.post(`${this.apiUrl}/${id}/index`);
  }

  askQuestion(id: number, question: string) {
    return axios.post(`${this.apiUrl}/${id}/ask`, null, {
      params: { question }
    });
  }

  retrieveContext(id: number, query: string, topK: number = 3) {
    return axios.get(`${this.apiUrl}/${id}/retrieve-context`, {
      params: { query, top_k: topK }
    });
  }

  deleteDocument(id: number) {
    return axios.delete(`${this.apiUrl}/${id}`);
  }
}