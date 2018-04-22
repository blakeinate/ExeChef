import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import {
  Recipe,
  RecipesService,
  User,
  UserService
} from '../shared';

@Component({
  selector: 'Recipe-page',
  templateUrl: './Recipe.component.html'
})
export class RecipeComponent implements OnInit {
  recipe: Recipe;
  currentUser: User;
  canModify: boolean;
  isSubmitting = false;
  isDeleting = false;

  constructor(
    private route: ActivatedRoute,
    private RecipesService: RecipesService,
    private router: Router,
    private userService: UserService,
  ) { }

  ngOnInit() {
    // Retreive the prefetched Recipe
    this.route.data.subscribe(
      (data: { recipe: Recipe }) => {
        console.log(data.recipe);
        this.recipe = data.recipe;
      }
    );
  
    // Load the current user's data
    this.userService.currentUser.subscribe(
      (userData: User) => {
        this.currentUser = userData;

        console.log(this.currentUser.username+"vs" + this.recipe.author.username);
        this.canModify = (this.currentUser.username === this.recipe.author.username);
      }
    );
  }

  onToggleFavorite(favorited: boolean) {
    this.recipe.in_favorites = favorited;
    if (favorited) {
      this.recipe.favorited_count++;
    } else {
      this.recipe.favorited_count--;
    }
  }

  onToggleFollowing(following: boolean) {
    this.recipe.author.am_i_following = following;
  }

  deleteRecipe() {
    this.isDeleting = true;
    this.RecipesService.destroy(this.recipe._id.$oid)
      .subscribe(
        success => {
          this.router.navigateByUrl('/');
        }
      );
  }
}
