import {Component, Input } from '@angular/core';

import { Recipe } from '../models';

@Component({
  selector: 'recipe-preview',
  templateUrl: './recipe-preview.component.html'
})
export class RecipePreviewComponent  {
  @Input() recipe: Recipe;




  onToggleFavorite(favorited: boolean) {
    this.recipe.in_favorites = favorited;

    if (favorited) {
      this.recipe.favorited_count++;
    } else {
      this.recipe.favorited_count--;
    }
  }
}
