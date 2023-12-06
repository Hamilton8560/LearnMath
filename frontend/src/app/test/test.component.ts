import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Question } from '../models/question.model';
import { TestService } from '../test.service';
import { UserService } from '../user.service';
import { ResultsComponent } from '../results/results.component';
import { User } from '../models/user.model';
@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit{
  testForm: FormGroup;
  questions: Question[]=[];
  userEmail:string;
  data:any;
  answered = false;
  userAnswers=[];
  showHint = {};
  difficulty
  constructor(private fb: FormBuilder, private router: Router, private http:HttpClient, private testService:TestService,
    private userService: UserService
    ) {}

  
  ngOnInit() {
    this.userService.userEmail.subscribe(email=>
      {
        this.userEmail = email;
      })
      this.userService.getUserdifficulty(this.userEmail).subscribe(
        (user:User) =>{
          console.log(user)
          this.difficulty = user.difficulty
          this.getQuestions();
        }
      )
   

    // Initialize showHint with false for each question
    this.questions.forEach((_, index) => {
      this.showHint[index] = false;
    });
    
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
    
    this.testService.getQuestions(this.userEmail,this.difficulty).subscribe(
      response => {
        
        this.questions = response.questions;
        
        console.log('Questions received:', this.questions);
      },
      error => {
        console.error('Error fetching questions:', error);
      }
    );
  }

 toggleHint(index: number) {
    this.showHint[index] = !this.showHint[index]; // Toggle hint visibility
  }

  onSubmit() {
    this.answered = true;
    this.data = [];
  
    for (let i = 0; i < this.questions.length; i++) {
      const question = this.questions[i];
      const userAnswer = this.testForm.value['answer' + (i + 1)];
      const isCorrect = userAnswer === question.answer;
      this.userAnswers.push(userAnswer); // Push each answer to userAnswers array
      console.log(this.userAnswers)
      this.data.push({
        email: this.userEmail,
        question: question.problem,
        correct: isCorrect
      });
    }
  
    this.testService.postQuestions(this.data);
  }


  refreshPage(): void {
    this.router.navigate(['home'])
  }

}
