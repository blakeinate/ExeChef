import {Profile} from './profile.model';

export class Comment{
  _id:{ $oid:string };
  body: string;
  created_date: { $date:string };
  user: Profile;
}
