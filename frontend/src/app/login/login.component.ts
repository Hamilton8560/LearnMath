import { Component } from '@angular/core';
import { Route, Router } from '@angular/router';
import { FormControl, FormGroup, Validators  } from '@angular/forms';
import { UserService } from '../user.service';
import { MessageService } from 'primeng/api';

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
formInvalid=false;

constructor(private router:Router, private userService: UserService, private messageService: MessageService){}

  ngOnInit(){
    this.registerForm=new FormGroup({
      firstName: new FormControl(''),
      lastName: new FormControl(''),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(5)]),
      passwordConfirm: new FormControl('')
    })

    this.loginForm=new FormGroup({
      email:new FormControl('', [Validators.required, Validators.email]),
      password:new FormControl('', [Validators.required, Validators.minLength(5)])
    })
  }
  
  onSubmit(){
   this.userService.authUser(this.loginForm.value).subscribe(
    response => 
    {
      this.messageService.add({ severity:'success', summary: 'Success', detail: 'Login Successful'})
      console.log("Login Successful:", response);
    },
    error => 
    {
      this.messageService.add({ severity:'error', summary: 'Fail', detail: 'Incorrect Login Information'})
      console.error("Login Failed:",error)
    }
   )

  }

  createAccount(){
    this.isAccountCreate=!this.isAccountCreate
  }


  newUser(){
    this.userService.checkUsername(this.registerForm.value.email).subscribe(
      response => {
        this.messageService.add({ severity:'warn', summary: 'Username Already Exists', detail: ''})
      },

      error => {
        if(this.registerForm.valid && this.registerForm.value.password == this.registerForm.value.passwordConfirm){
         
          this.userService.createUser(this.registerForm.value).subscribe(
            response => 
            {
              this.messageService.add({ severity:'success', summary: 'Success', detail: 'Profile Successfully Created'})
              console.log("Successfully Created", response);
              this.createAccount();
            },
            error => 
            {
              const detail = error.error && error.error.response ? error.error.response : 'Unexpected error occurred';
              this.messageService.add({ severity:'error', summary: 'Fail', detail: detail})
              console.error("Failed:", error)
            })
          

        }
        else{
        this.formInvalid= true;
      }
      }
    )


}

}
