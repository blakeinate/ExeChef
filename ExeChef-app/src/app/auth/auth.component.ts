import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router} from '@angular/router';
import { Errors, UserService } from '../shared';

@Component({
  selector: 'auth-page',
  templateUrl: './auth.component.html'
})
export class AuthComponent implements OnInit {
  authType: String = '';
  title: String = '';
  errors: Errors = new Errors();
  isSubmitting: boolean = false;
  authForm: FormGroup;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService,
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
    this.errors = new Errors();

    let credentials = this.authForm.value;
    //if were logging in then let credentials be in the form of login, Password
    // so user can use username to login
    if(this.authType == "login"){
     credentials = {
        "login": credentials.email,
        "password": credentials.password
      }
    }
    this.userService.attemptAuth(this.authType,credentials).subscribe(
      (data)=>{
        console.log("from auth component ",data);
        this.router.navigateByUrl('/');
      },
      (err)=>{
        this.errors = {
          errors: {"Error":err.message}
      };
        console.log("errors->",err);
        console.log(this.errors);
        this.isSubmitting = false;
      }
    )
    console.log(credentials);
  }
}
