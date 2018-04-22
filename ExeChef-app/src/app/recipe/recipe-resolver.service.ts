import { Injectable, } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, Router, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs/Rx';

import { Recipe, RecipesService, UserService } from '../shared';

@Injectable()
export class RecipeResolver implements Resolve<Recipe> {
  constructor(
    private recipesService: RecipesService,
    private router: Router,
    private userService: UserService
  ) {}

  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any> {

    return this.recipesService.get(route.params['recipe_id'])
           .catch((err) => this.router.navigateByUrl('/'));

  }
}
