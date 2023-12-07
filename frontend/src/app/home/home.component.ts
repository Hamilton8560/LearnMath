import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
user
  constructor(private router:Router,private userService:UserService){
    this.user == this
  }

  onClick(){
    this.router.navigate(['test'])
  }
}
