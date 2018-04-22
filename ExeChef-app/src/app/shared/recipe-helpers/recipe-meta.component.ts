import { Component, Input } from '@angular/core';

import { Recipe } from '../models';

@Component({
  selector: 'recipe-meta',
  templateUrl: './recipe-meta.component.html'
})
export class RecipeMetaComponent {
  @Input() recipe: Recipe;
}
