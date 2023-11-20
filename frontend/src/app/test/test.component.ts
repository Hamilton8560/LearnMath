import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit{
  testForm: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
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

  onSubmit() {

    //Not sure if this part is correct
    const answers = this.testForm.value;
    console.log(answers);

  }

  refreshPage(): void {
    window.location.reload();
  }

}