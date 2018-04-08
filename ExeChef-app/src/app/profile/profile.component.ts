import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { User, UserService, Profile } from '../shared';

@Component({
  selector: 'profile-page',
  templateUrl: './profile.component.html'
})
export class ProfileComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private userService: UserService
  ) {}

  profile: Profile;
  currentUser: User;
  isUser: boolean;

  ngOnInit() {
    this.route.data.subscribe(
      (data) => {
        this.profile = data.profile.user;
        console.log("The user profile we are looking at -->",this.profile.username);
        this.getCurrentUser();
      }
    );
     //console.log("The current user that is logged in -->",this.userService.getCurrentUser().username);
      //this.isUser = (this.userService.getCurrentUser().username === this.profile.username);
    // Load the current user's data

  }

  getCurrentUser(){
    this.userService.currentUser.subscribe(
      (userData: User) => {
        this.currentUser = userData;
        console.log("The current user that is logged in -->",this.currentUser.username);

        this.isUser = (this.currentUser.username === this.profile.username);
      }
    );
  }
  onToggleFollowing(following: boolean) {
    this.profile.following = following;
  }

}
