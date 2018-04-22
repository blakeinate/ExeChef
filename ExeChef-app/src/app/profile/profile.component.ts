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
        this.getCurrentUser();

      }
    );
  }

  getCurrentUser(){
    this.userService.currentUser.subscribe(
      (userData: User) => {
        this.currentUser = userData;
        this.isUser = (this.currentUser.username === this.profile.username);
      }
    );
  }
  onToggleFollowing(following: boolean) {
    this.profile.am_i_following = following;
  }

}
