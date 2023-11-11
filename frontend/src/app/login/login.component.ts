import { Component } from '@angular/core';
import { Route, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
loginForm:FormGroup;
isAccountCreate=false;
registerForm:FormGroup;
mine

constructor(private router:Router){}

  ngOnInit(){
    this.registerForm=new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(5)]),
      passwordConfirm: new FormControl('')
    })

    this.loginForm=new FormGroup({
      email:new FormControl(''),
      password:new FormControl('')
    })
  }
  
  onSubmit(){
    console.log(this.loginForm.value)
  }
  createAccount(){
    console.log(this.registerForm.value)
    this.isAccountCreate=!this.isAccountCreate
  }

}
