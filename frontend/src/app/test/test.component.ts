import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Question } from '../models/question.model';
import { TestService } from '../test.service';
@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit{
  testForm: FormGroup;
  questions: Question[]=[];
    
  

  constructor(private fb: FormBuilder, private router: Router, private http:HttpClient, private testService:TestService) {}

  
  ngOnInit() {
    this.getQuestions();
    
    this.testForm = this.fb.group({
      answer1: ['', Validators.required],
      answer2: ['', Validators.required],
      answer3: ['', Validators.required],
      answer4: ['', Validators.required],
      answer5: ['', Validators.required],
      answer6: ['', Validators.required],
      answer7: ['', Validators.required],
      answer8: ['', Validators.required],
      answer9: ['', Validators.required],
      answer10: ['', Validators.required]
    });
  }
  getQuestions(){
    this.testService.getQuestions().subscribe(
      response => {
        
        this.questions = response.questions;
        
        console.log('Questions received:', this.questions);
      },
      error => {
        console.error('Error fetching questions:', error);
      }
    );
  }

  onSubmit() {
    this.testService.postQuestions().subscribe(
      response=>{
        console.log(response)
      }
    )
  }


  refreshPage(): void {
    window.location.reload();
  }

}