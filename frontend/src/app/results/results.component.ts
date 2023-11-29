import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent {
@Input() resultsData:any;
@Input() userAnswers: any[];
grade

constructor(){}

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
  const percent = (correctCount/totalItems)*100;
  this.grade = Math.round(percent)

}
refreshPage(): void {
  window.location.reload();
}
}
