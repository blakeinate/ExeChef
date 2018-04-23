import { Injectable } from '@angular/core';
import { URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService} from './api.service';
import { UserService} from './user.service';
import { Recipe, User,RecipeListConfig } from '../models';

@Injectable()
export class RecipesService {
  constructor (
    private apiService: ApiService,
    private userService: UserService,
  ) {}

  /**
  * type field will take a type of option
  * global- will to get the global feed ( all recipes)
  * user - wiill be to get the users feed based on people he follows
  * created - will be to get users recipes that he created
  * favorites - will be to get the users recipes that he favorited
  * tag - will to get recipes with matching tags
  * limit field will be a limt to the amount a user wants from the request default is 10 if no limit is provided
  * query feild will apply for searchs
  *
  */
  query(config:RecipeListConfig): Observable<Recipe[]>{
        let request;
        if(config.type == "global"){
          request = config.limit != 10? `/Feed/${config.limit}`: `/Feed` ;
          return this.apiService.getWithoutToken(request)
          .map(data => data.recipes);
        }
        else if(config.type === "user"){
          request = config.limit != 10? `/Feed/${config.limit}`: `/Feed`;
        }
        else if (config.type === "created"){
          request = config.limit != 10? `/Recipe/Created/${config.limit}`: `/Recipe/Created` ;
        }
        else if( config.type === "favorites"){
          request = config.limit != 10? `/Recipe/Favorites/${config.limit}`: `/Recipe/Favorites` ;
        }
        else if(config.type === "tag"){
          request = config.limit != 10? `/SearchTags/${config.query}/${config.limit}`: `/SearchTags/${config.query}` ;
        }
        if(config.type !== "global"){
          return this.apiService.get(request)
          .map(data => data.recipes);
        }
  }

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
