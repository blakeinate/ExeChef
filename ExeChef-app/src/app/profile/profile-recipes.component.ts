import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { RecipeListConfig, Profile } from '../shared';

@Component({
  selector: 'profile-recipes',
  templateUrl: './profile-recipes.component.html'
})
export class ProfileRecipesComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  profile: Profile;
  recipesConfig: RecipeListConfig = new RecipeListConfig();

  ngOnInit() {
    this.route.parent.params.subscribe(
      (data)=>  this.recipesConfig.profile_name = data.username
    )
    this.route.url.subscribe(
      (data) => {
        let type = data[data.length - 1].path;
        this.recipesConfig.type = type;

        console.log("only fire when im clicked");
      }
    );
  }

}
