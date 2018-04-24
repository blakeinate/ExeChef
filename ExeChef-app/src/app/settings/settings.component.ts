import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

import { User,Settings, UserService } from '../shared';

@Component({
  selector: 'settings-page',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})

export class SettingsComponent implements OnInit{
  image:any;
  user: User = new User();
  settings: Settings = new Settings();
  settingsForm: FormGroup;
  errors: Object = {};
  isSubmitting: boolean = false;

  constructor(
    private router: Router,
    private userService: UserService,
    private fb: FormBuilder
  ){
    this.settingsForm = this.fb.group({

      //username: '',
      bio: '',
      email: '',
      old_password: '',
      new_password: '',
      image: null,
    });
  }
  ngOnInit(){
    (<any>Object).assign(this.user,this.userService.getCurrentUser());
    this.settingsForm.patchValue(this.user);
  }
  onFileChange(event) {
    let fileList: FileList = event.target.files;
       if(fileList.length > 0) {
           let file: File = fileList[0];
           let formData:FormData = new FormData();
           formData.append('uploadFile', file, file.name);
            this.userService.updateImage(formData).subscribe(
              user =>{
              }
            )
       }
 }
 //  onFileChange(event) {
 //   let reader = new FileReader();
 //   if(event.target.files && event.target.files.length > 0) {
 //     let file = event.target.files[0];
 //     reader.readAsDataURL(file);
 //     reader.onload = () => {
 //       let formData:FormData = new FormData();
 //       console.log(file,file.name);
 //       formData.append('uploadFile', file, file.name);
 //        this.userService.updateImage(formData).subscribe(
 //          user =>{
 //          })
 //     };
 //   }
 // }

  logout(){
    this.userService.purgeAuth();
    this.router.navigateByUrl('/');
  }

  submitForm(){
    this.isSubmitting = true;

    this.updateSettings(this.settingsForm.value);
    (<any>Object).assign(this.settings,this.image);
    this.userService.update(this.settings).subscribe(
      updatedUser => {
        this.router.navigateByUrl('/profile/'+ updatedUser.username)
      },
      err =>{
        this.errors = {
          errors: {"Error":err.message}
        };
        this.isSubmitting = false;
      }
    )
  }

  updateSettings(updatedSettings:Settings){

    if(this.user.email === updatedSettings.email){

      updatedSettings.email = "";
    }
    (<any>Object).assign(this.settings,updatedSettings);
  }


}
