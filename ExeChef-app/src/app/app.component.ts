import { Component, OnInit } from '@angular/core';


import { UserService } from './shared';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit {
  constructor(
    private userService: UserService
  ){}

  ngOnInit(){
    this.userService.populate();
    this.userService.isAuthenticated.subscribe(isAuth => {
      if(isAuth){
        this.refresh();
      }
    });
  }

  refresh(){
    setTimeout(()=>{
      this.userService.refresh();
      console.log("refreshing tokens");
      this.refresh();
    },600000)
  }
}
