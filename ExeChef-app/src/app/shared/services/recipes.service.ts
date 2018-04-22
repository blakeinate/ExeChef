import { Injectable } from '@angular/core';
import { URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService} from './api.service';
import { UserService} from './user.service';
import { Recipe, User } from '../models';

@Injectable()
export class RecipesService {
  constructor (
    private apiService: ApiService,
    private userService: UserService,
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

  destroy(recipe_id:string){
   return this.apiService.delete('/Recipe/' + recipe_id)
  }

  toggleFavorite(recipe_id:string):Observable<User>{
     var favorites = this.userService.getCurrentUser().favorites;
     var emit = false;
     //console.log(this.userService.getCurrentUser());
     console.log(recipe_id);
     if(favorites == null){
       favorites = [];
     }
     if(!favorites.includes(recipe_id)){
          favorites.push(recipe_id);
          emit = true;
        }else{
          favorites = favorites.filter(removeRecipeID => recipe_id !== removeRecipeID);
        }
        return this.userService.update({favorites:favorites}).map(data=>{
          console.log({favorites:favorites});
          //pass back a value for button to emit;
        data["emit"] = emit;
        return data;
    })
  }


}
