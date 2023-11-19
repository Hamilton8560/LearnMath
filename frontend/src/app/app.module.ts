import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ButtonModule } from 'primeng/button';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from '../app/login/login.component'
import { RouterModule } from '@angular/router';
import { CardModule } from 'primeng/card';
import {ReactiveFormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ToastModule } from 'primeng/toast';
import { MessagesModule } from 'primeng/messages';
import { MessageService } from 'primeng/api';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
  
  ],
  imports: [
    BrowserModule,
    ButtonModule,
    AppRoutingModule,
    RouterModule,
    CardModule,
    ReactiveFormsModule,
    InputTextModule,
    HttpClientModule,
    BrowserAnimationsModule,
    ToastModule,
    MessagesModule
    
  ],
  providers: [ MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
