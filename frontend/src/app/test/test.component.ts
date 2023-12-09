import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { TestService } from '../test.service';
import { UserService } from '../user.service';
import { Question } from '../models/question.model';
import { User } from '../models/user.model';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {
  
  testForm: FormGroup;
  questions: Question[] = [];
  userEmail: string;
  data: any;
  answered = false;
  userAnswers = [];
  showHint = {};
  difficulty: number;
  hintCount = 0;

  constructor(
    private fb: FormBuilder, 
    private router: Router, 
    private testService: TestService,
    private userService: UserService
  ) {}

  ngOnInit(): void {
    // Subscribe to user email and difficulty
    this.initializeDifficulty();

    // Initialize form with dynamic form controls
    this.initializeForm();
  }

  private initializeDifficulty(){
    this.userService.userEmail.subscribe(email => this.userEmail = email);
    this.userService.getUserdifficulty(this.userEmail).subscribe(
      (user: User) => {
        this.difficulty = user.user.difficulty;
        this.getQuestions();
      }
    );
  }

  private initializeForm(): void {
    const formGroup = {};
    for (let i = 1; i <= 10; i++) {
      formGroup['answer' + i] = ['', Validators.required];
    }
    this.testForm = this.fb.group(formGroup);
  }

  private getQuestions(): void {
    this.testService.getQuestions(this.userEmail, this.difficulty).subscribe(
      response => {
        this.questions = response.questions;
        // Initialize showHint for each question
        this.questions.forEach((_, index) => this.showHint[index] = false);
      },
      error => console.error('Error fetching questions:', error)
    );
  }

  toggleHint(index: number): void {
    if (!this.showHint[index]) this.hintCount++;
    this.showHint[index] = !this.showHint[index];
  }

  onSubmit(): void {
    this.answered = true;
    this.data = this.questions.map((question, i) => {
      const userAnswer = this.testForm.value['answer' + (i + 1)];
      this.userAnswers.push(userAnswer);
      return {
        email: this.userEmail,
        question: question.problem,
        correct: userAnswer === question.answer
      };
    });
    this.testService.postQuestions(this.data);
  }

  refreshPage(): void {
    this.router.navigate(['home']);
  }

  onClickHintAnswer(hint: string, index: number): void {
    this.testForm.patchValue({ ['answer' + (index + 1)]: hint });
  }

  receiveDataFromChild(): void {
    this.answered = !this.answered;
  }

  toggleAnswered(): void {
    this.router.navigate(['home']);
    /*this.initializeDifficulty();
    this.initializeForm()
    this.answered = !this.answered;*/
  }
}
