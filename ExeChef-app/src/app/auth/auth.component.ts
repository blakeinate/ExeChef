import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'auth-page',
  templateUrl: './auth.component.html'
})
export class AuthComponent implements OnInit {
  authType: String = '';
  title: String = '';
  isSubmitting: boolean = false;
  authForm: FormGroup;

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder
  ) {
    // use FormBuilder to create a form group
    this.authForm = this.fb.group({
      'email': ['', Validators.required],
      'password': ['', Validators.required]
    });
  }

  ngOnInit() {
    this.route.url.subscribe(data => {
      // Get the last piece of the URL (it's either 'login' or 'register')
      this.authType = data[data.length - 1].path;
      // Set a title for the page accordingly
      this.title = (this.authType === 'login') ? 'Sign In' : 'Sign Up';
      // add form control for username if this is the register page
      if (this.authType === 'register') {
        this.authForm.addControl('username', new FormControl('', Validators.required));
      }
    });
  }

  submitForm() {
    this.isSubmitting = true;

    let credentials = this.authForm.value;
    // check out what you get!
    console.log(credentials);
  }
}
