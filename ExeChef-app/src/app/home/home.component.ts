import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { RecipeListConfig, RecipesService, UserService } from '../shared';

 @Component({
   selector: 'home-page',
   templateUrl: './home.component.html',
   styleUrls: ['./home.component.scss']
 })
export class HomeComponent implements OnInit {
   constructor(
    private router: Router,
    private recipesService: RecipesService,
    private userService: UserService
   ) {}

  isAuthenticated: boolean;
  listConfig: RecipeListConfig = new RecipeListConfig();
  tags: Array<string> = [];
  tagsLoaded: boolean = false;

  ngOnInit() {

    this.userService.isAuthenticated.subscribe(
      (authenticated) => {
        this.isAuthenticated = authenticated;

        // set the article list accordingly
        if (authenticated) {
          this.setListTo('user');
        } else {
          this.setListTo('global');
        }
      }
    );

    // this.tagsService.getAll()
    // .subscribe(tags => {
    //   this.tags = tags;
    //   this.tagsLoaded = true;
    // });
  }
  onEnter(search){
    this.setListTo("tag",search);
  }

  setListTo(type: string = '',tag:string ="") {
    this.listConfig = new RecipeListConfig();

    // If feed is requested but user is not authenticated, redirect to login
    if (type === 'feed' && !this.isAuthenticated) {
      this.router.navigateByUrl('/login');
      return;
    }
    if(type === 'tag'){
      this.listConfig.query = tag;
    }
    console.log('setting to ',type);
    // Otherwise, set the list object
    this.listConfig.type =type;
  }
 }
