import { Routes } from '@angular/router';
import { UploadComponent } from './components/upload/upload.component';
import { DocumentsComponent } from './components/documents/documents.component';
import { ChatComponent } from './components/chat/chat.component';

export const routes: Routes = [
  { path: 'upload', component: UploadComponent },
  { path: 'documents', component: DocumentsComponent },
  { path: 'chat/:id', component: ChatComponent },
  { path: '', redirectTo: '/documents', pathMatch: 'full' }
];
