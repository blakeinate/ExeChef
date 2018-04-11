import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl,FormArray } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Recipe, RecipesService } from '../shared';

@Component({
  selector: 'editor-page',
  templateUrl: './editor.component.html'
})
export class EditorComponent implements OnInit {


  //********LEFT TO DO****/
  //add ingredient form
  //patch existing steps that might already exist
  //patch existing tags and steps that might exist from a pre existing article

  recipe: Recipe = new Recipe();
  recipeForm: FormGroup;
  ingredients: FormGroup;
  tagField = new FormControl();
  stepField = new FormControl();
  units: Array<string> = [
    "teaspoon",
    "tablespoon",
    "fluid ounce",
    "gill",
    "cup",
    "pint",
    "quart",
    "gallon",
    "ml",
    "l",
    "dl",
    "pound",
    "ounce",
    "mg",
    "g",
    "kg",
    "mm",
    "cm",
    "m",
    "inch",
    "bag",
    "jar",
  ];
  errors: Object = {};
  isSubmitting: boolean = false;

  constructor(
    private recipesService: RecipesService,
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder
  ) {
    // use the FormBuilder to create a form group
    this.recipeForm = this.fb.group({
      title: '',
      description: '',
      ingredients: this.fb.array([
        this.initIngredients(),
      ]),
      private: false,
    });
    // Optional: subscribe to value changes on the form
    // this.recipeForm.valueChanges.subscribe(value => this.updateArticle(value));




  }

  initIngredients(){
    return this.fb.group({
      name:'',
      amount:'',
      unit:''
    })
  }

  addIngredients(){
    const control = <FormArray>this.recipeForm.controls["ingredients"];
    control.push(this.initIngredients());
  }
  removeIngredients(index:number){
    const control = <FormArray>this.recipeForm.controls["ingredients"];
    control.removeAt(index);
  }

  ngOnInit() {
    // If there's an recipe prefetched, load it
    this.route.data.subscribe(
      (data: {recipe: Recipe}) => {
        if (data.recipe) {
          this.recipe = data.recipe;
          this.recipeForm.patchValue(data.recipe);
        }
      }
    );
  }

  addTag() {
    // retrieve tag control
    let tag = this.tagField.value;
    // only add tag if it does not exist yet
    if (this.recipe.tags.indexOf(tag) < 0) {
      this.recipe.tags.push(tag);
    }
    // clear the input
    this.tagField.reset('');
  }

  removeTag(tagName: string) {
    this.recipe.tags = this.recipe.tags.filter((tag) => tag !== tagName);
  }

  addStep() {
    // retrieve tag control
    let step = this.stepField.value;
    this.recipe.steps.push(step);
    // clear the input
    this.stepField.reset('');
  }

  changeStep(index: number,step:string){
    this.recipe.steps[index] = step;
  }

  removeStep(index: number) {
    this.recipe.steps.splice(index,1);
  }


  updateRecipe(values: Object) {
    (<any>Object).assign(this.recipe, values);
  }

  submitForm() {
    this.isSubmitting = true;
    //console.log("This is the recipe object im sending",this.recipeForm.value);
    // // update the model
    this.updateRecipe(this.recipeForm.value);
    console.log("this is the recipe object that i am sending",this.recipe);
    //
    // // post the changes
    // this.recipesService
    // .save(this.recipe)
    // .subscribe(
    //   recipe => this.router.navigateByUrl('/Recipe/' + recipe.recipe_id),
    //   err => {
    //     this.errors = err;
    //     this.isSubmitting = false;
    //   }
    // );
  }
}
