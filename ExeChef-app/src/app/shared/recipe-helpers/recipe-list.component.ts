import { Component, Input } from '@angular/core';

import { Recipe, RecipeListConfig } from '../models';
import { RecipesService } from '../services';

@Component({
  selector: 'recipe-list',
  templateUrl: './recipe-list.component.html',
  styleUrls: ['./recipe-meta.component.scss']
})
export class RecipeListComponent {
  constructor (
    private recipesService: RecipesService
  ) {}

  listConfig: RecipeListConfig;
  results: Recipe[];
  loading: boolean = false;


  @Input()
  set config(config: RecipeListConfig) {
    if (config) {
      this.listConfig = config;
      this.runQuery();
    }
  }


runQuery() {
  console.log(this.listConfig.type);

    this.loading = true;
    this.results = [];

    this.recipesService.query(this.listConfig)
     .subscribe(recipes => {
       console.log(recipes);
        this.loading = false;
        this.results = recipes

        // Used from http://www.jstips.co/en/create-range-0...n-easily-using-one-line/
    });
}

  // setPageTo(pageNumber) {
  //   this.currentPage = pageNumber;
  //   this.runQuery();
  // }
}
