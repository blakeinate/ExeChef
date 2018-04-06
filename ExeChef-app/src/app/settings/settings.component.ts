import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

import { User, UserService } from '../shared';

@Component({
  selector: 'settings-page',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})

export class SettingsComponent implements OnInit{

  user: User = new User();
  settingsForm: FormGroup;
  errors: Object = {};
  isSubmitting: boolean = false;

  constructor(
    private router: Router,
    private userService: UserService,
    private fb: FormBuilder
  ){
    this.settingsForm = this.fb.group({
      image: '',
      username: '',
      bio: '',
      email: '',
      password: '',
    });
  }
  ngOnInit(){
    (<any>Object).assign(this.user,this.userService.getCurrentUser());
    this.settingsForm.patchValue(this.user);
  }

  logout(){
    this.userService.purgeAuth();
    this.router.navigateByUrl('/');
  }

  submitForm(){
    this.isSubmitting = true;

    this.updateUser(this.settingsForm.value);

    this.userService.update(this.user).subscribe(
      updatedUser => this.router.navigateByUrl('/profile/'+ updatedUser.username),
      err =>{
        this.errors = {
          errors: {"Error":err.message}
        };
        this.isSubmitting = false;
      }
    )
  }

  updateUser(updatedUser:User){
    (<any>Object).assign(this.user,updatedUser);
  }


}
