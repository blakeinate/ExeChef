import { Injectable } from '@angular/core';
import { URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService } from './api.service';
import { Recipe } from '../models';

@Injectable()
export class RecipesService {
  constructor (
    private apiService: ApiService
  ) {}

  get(recipe_id:string): Observable<Recipe> {
    return this.apiService.get('/Recipe/' + recipe_id)
           .map(data => data.recipe);
  }

  save(recipe): Observable<Recipe> {
    // If we're updating an existing article
    if (recipe.recipe_id) {
      return this.apiService.put('/Recipe/' + recipe._id, {recipe: recipe})
             .map(data => data.recipe);

    // Otherwise, create a new article
    } else {
      return this.apiService.post('/Recipe', {recipe: recipe})
             .map(data => data.recipe);

    }
  }

}
