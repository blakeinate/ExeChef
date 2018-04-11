import {Profile }from './profile.model';
import {Ingredient}from './ingredient.model';

export class Recipe{
    recipe_id:string;
    name : string;
    image_name: string;
    tags: Array<string> = [];
    steps : Array<string> = [];
    author : Profile;
    description : string;
    private : boolean;
    ingredients : Array<Ingredient> = [];
    created_date : Date;
    modified_date : Date;
}
