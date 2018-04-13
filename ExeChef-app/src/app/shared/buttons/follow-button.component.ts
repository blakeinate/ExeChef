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
    console.log(profile);
    this.profile = profile;
    this.userService.isAuthenticated.subscribe(
      (authenticated) =>{
        if(!authenticated){
          profile.following = false;
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



          this.userService.currentUser.subscribe(
            (userData: User) => {
              this.followingList = userData.followers;
             console.log("follow list",this.followingList);
             console.log("user we want to follow",this.profile.username);
                // Follow this profile if we aren't already
              if(!this.followingList.includes(this.profile.username)){
                this.followingList.push(this.profile.username);
                this.profilesService.follow(this.followingList)
                .subscribe(
                  data => {
                    this.isSubmitting = false;
                    this.onToggle.emit(true);
                  },
                  err => this.isSubmitting = false
                );
              }else{
                  // Otherwise, unfollow this profile
                this.followingList = userData.followers.filter(username => this.profile.username !== username);
                //console.log("unfollow",this.followingList);
                this.profilesService.follow(this.followingList)
                .subscribe(
                  data => {
                    this.isSubmitting = false;
                    this.onToggle.emit(false);
                  },
                  err => this.isSubmitting = false
                );
              }
            }
          );
        }
    )
  }

}
