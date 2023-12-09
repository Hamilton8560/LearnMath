import { Component } from '@angular/core';
import { UserService } from '../user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {

constructor(private userService:UserService){
  this.userService.getUser('david@email.com').subscribe(
    response=>console.log(response)
  )
}
}