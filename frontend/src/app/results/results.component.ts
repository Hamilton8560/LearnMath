import { Component, OnInit, EventEmitter, Output, Input } from '@angular/core';
import { TestService } from '../test.service';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {
  @Output() dataEmitter: EventEmitter<any> = new EventEmitter();
  @Input() resultsData: any;
  @Input() userAnswers: any[];
  @Input() totalHints: number;
  @Input() difficulty: number;
  @Input() userEmail: string;
  grade: number;

  constructor(private testService: TestService, private userService: UserService, private router: Router) {}

  ngOnInit(): void {
    this.calculateGrade();
  }

  private calculateGrade(): void {
    const totalItems = this.resultsData.length;
    const correctCount = this.resultsData.filter(item => item.correct).length;
    const percent = (correctCount / totalItems) * 100 - (this.totalHints * 2);
    this.updateDifficultyIfNeeded(percent);
    this.grade = Math.round(percent);
  }

  private updateDifficultyIfNeeded(percent: number): void {
    if (percent > 85 && this.difficulty < 7) {
      this.updateDifficulty(this.difficulty + 1);
    } else if (percent < 69 && this.difficulty > 1) {
      this.updateDifficulty(this.difficulty - 1);
    }
  }

  private updateDifficulty(newDifficulty: number): void {
    this.userService.patchDifficulty(this.userEmail, newDifficulty)
      .subscribe(
        response => {
          console.log('Difficulty updated:', response);
          this.userService.setUserDifficulty(newDifficulty);
        },
        error => console.error('Error updating difficulty:', error)
      );
  }

  refreshPage(): void {
    this.router.navigate(['test']);
  }

  sendDataToParent(): void {
    this.dataEmitter.emit();
  }

  onChangeDifficulty(newDifficulty: number): void {
    this.updateDifficulty(newDifficulty);
  }
}
