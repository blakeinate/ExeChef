import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

import { Profile, User } from '../models';
import { ProfilesService, UserService } from '../services';

@Component({
  selector: 'follow-button',
  templateUrl: './follow-button.component.html'
})
export class FollowButtonComponent {
  constructor(
    private profilesService: ProfilesService,
    private router: Router,
    private userService: UserService
  ) {

  }

  profile:Profile;
  @Input() set profileInput(profile: Profile){
    console.log("coming from follow button",profile);
    this.profile = profile;
    this.userService.isAuthenticated.subscribe(
      (authenticated) =>{
        if(!authenticated){
          console.log("not auth: viewing follow page");
          profile.am_i_following = false;
        }
      }
    )
  }
  @Output() onToggle = new EventEmitter<boolean>();
  isSubmitting = false;
  followingList:string[];

  toggleFollowing() {
    this.isSubmitting = true;

    this.userService.isAuthenticated.subscribe(
      (authenticated) => {
        // Not authenticated? Push to login screen
        if (!authenticated) {
          this.router.navigateByUrl('/login');
          return;
        }



        this.profilesService.toggleFollowing(this.profile.username)
        .subscribe(
          data => {
            this.isSubmitting = false;
            this.onToggle.emit(data["emit"]);
          },
          err => this.isSubmitting = false
        );
        }
    )
  }

}
