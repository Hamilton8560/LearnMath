import { Component } from '@angular/core';
import { Route, Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent {
id: number;
rawText = 'Hello, this is raw text!';
buttonColor: string;

  generateRandomColor() {
    // Generate a random hexadecimal color
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    this.buttonColor = color;
  }

constructor(private router:Router){}

  onButtonClick() {
    this.generateRandomColor();
  }
  onStart(id:number){
    this.router.navigate(['/test', id]);
  }

}
