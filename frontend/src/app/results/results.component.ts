import { Component, OnInit, EventEmitter, Output, Input  } from '@angular/core';
import { TestService } from '../test.service';
import { UserService } from '../user.service';
import { response } from 'express';
@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent {
@Output() dataEmitter: EventEmitter<any> = new EventEmitter();
@Input() resultsData:any;
@Input() userAnswers: any[];
@Input() totalHints:number;
@Input() difficulty:number;
@Input() userEmail:string;
email
grade

constructor(private testService:TestService,private userService:UserService){}

ngOnInit(){
  console.log(this.userAnswers)
  this.getGrade();
 
}

getGrade(){
  const totalItems = this.resultsData.length;
  let correctCount = 0;

  this.resultsData.forEach(item =>{
    if (item.correct === true){
      correctCount++
    }
  });
  const percent = (correctCount/totalItems)*100 - (this.totalHints*2);
  if(percent > 85 && this.difficulty < 7)
  {
    this.testService.patchDifficulty(this.userEmail, this.difficulty+1)
    .subscribe(response=>
      console.log(response)
      )
      error=>
      {
        console.log(error)
      }
    
  }
  if (percent < 69 && this.difficulty > 1)
  {
    this.testService.patchDifficulty(this.email, this.difficulty-1)
    .subscribe( response =>
      console.log(response)
      )
      error =>
      {
        console.log(error)
      }
  }

  this.grade = Math.round(percent)

}
refreshPage(): void {
  window.location.reload();
}

sendDataToParent() 
{
  this.dataEmitter.emit();
}
}
