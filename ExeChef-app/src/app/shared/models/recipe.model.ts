import {Profile }from './profile.model';
import {Ingredient}from './ingredient.model';

export class Recipe{
    name : string;
    image_name: string;
    tags: string[];
    steps : string[];
    author : Profile;
    description : string[];
    private : boolean;
    ingredients : Ingredient[];
    created_date : Date;
    modified_date : Date;
}
