import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl,FormArray } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Recipe, RecipesService, Unit } from '../shared';

@Component({
  selector: 'editor-page',
  templateUrl: './editor.component.html'
})
export class EditorComponent implements OnInit {


  //********LEFT TO DO****/
  //patch existing steps that might already exist
  //patch existing tags and steps that might exist from a pre existing article
  //FIX bug with duplicate slider movement

  recipe: Recipe = new Recipe();
  recipeForm: FormGroup;
  ingredients: FormGroup;
  tagField = new FormControl();
  stepField = new FormControl();
  unitStep:number = 100;
  unitMax: number = 100;
  unitValue:number = 50;
  unitLabel: string;
  units: Array<Unit> = [
    {
      name:"teaspoon",
      abrev: "tsp",
      max: 20,
      step: .25
    },
    {
      name:"tablespoon",
      abrev: "tbsp",
      max: 20,
      step: .25
    },
    {
      name:"fluid ounce",
      abrev: "oz",
      max: 500,
      step: 1
    },
    {
      name:"gill",
      abrev:"gill",
      max: 500,
      step: 1
    },
    {
      name:"cup",
      abrev:"cup",
      max: 100,
      step: .25
    },
    {
      name:"pint",
      abrev:"pt",
      max: 100,
      step: .25
    },
    {
      name:"quart",
      abrev:"qt",
      max: 100,
      step: .25
    },
    {
      name:"gallon",
      abrev:"gal",
      max: 100,
      step: .5
    },
    {
      name:"milliliter",
      abrev:"ml",
      max: 200,
      step: .5
    },
    {
      name:"liter",
      abrev:"l",
      max: 200,
      step: .5
    },
    {
      name:"deciliter",
      abrev:"dL",
      max: 200,
      step: .5
    },
    {
      name:"pound",
      abrev:"lb",
      max: 200,
      step: 1
    },
    {
      name:"ounce",
      abrev:"oz",
      max: 200,
      step: .5
    },
    {
      name:"milligram",
      abrev:"mg",
      max: 200,
      step: .25
    },
    {
      name:"gram",
      abrev:"g",
      max: 500,
      step: .25
    },
    {
      name:"kilogram",
      abrev:"kg",
      max: 500,
      step: .25
    },
    {
      name:"millimeter",
      abrev:"mm",
      max: 1000,
      step: .25
    },
    {
      name:"centimeter",
      abrev:"cm",
      max: 1000,
      step: .25
    },
    {
      name:"meter",
      abrev:"m",
      max: 1000,
      step: 1
    },
    {
      name:"inch",
      abrev:"in",
      max: 20,
      step: .25
    },
    {
      name:"bag",
      abrev:"bag",
      max: 100,
      step: .25
    },
    {
      name:"jar",
      abrev:"jar",
      max: 100,
      step: .25
    },
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
      name: '',
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

  setSlider(input:any){
    let name = input.srcElement.value;
    let index = this.units.findIndex(unit => unit.name === name);
    if(index > -1){
      let unit = this.units[index];
      this.unitStep = unit.step;
      this.unitMax = unit.max;
      this.unitValue = unit.max/2;
      this.unitLabel = unit.abrev;
    }else{
        this.unitLabel = name;
    }

  }
  changeLabel(input:any){
      this.unitValue = input.srcElement.value;

  }

  submitForm() {
    this.isSubmitting = true;
    //console.log("This is the recipe object im sending",this.recipeForm.value);
    // // update the model
    this.updateRecipe(this.recipeForm.value);
    console.log("this is the recipe object that i am sending",this.recipe);

    // post the changes
    this.recipesService
    .save(this.recipe)
    .subscribe(
      //recipe => console.log(recipe),
     recipe => this.router.navigateByUrl('/Recipe/' + recipe._id),
      err => {
        this.errors = err;
        this.isSubmitting = false;
      }
    );
  }
}
