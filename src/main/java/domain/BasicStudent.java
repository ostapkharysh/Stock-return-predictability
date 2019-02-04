package domain;

import json.*;

/**
 * Created by Andrii_Rodionov on 1/5/2017.
 */
public class BasicStudent implements Jsonable {

    protected String name;
    protected String surname;
    protected Integer year;

    public BasicStudent() {
    }

    public BasicStudent(String name, String surname, Integer year) {
        this.name = name;
        this.surname = surname;
        this.year = year;
    }

    @Override
    public JsonObject toJsonObject() {
        JsonString jsonName = new JsonString(this.name);
        JsonPair name = new JsonPair("name", jsonName);
        JsonString jsonSurname = new JsonString(this.surname);
        JsonPair surname = new JsonPair("surname", jsonSurname);
        JsonNumber jsonYear = new JsonNumber(this.year);
        JsonPair year = new JsonPair("year", jsonYear);
        return new JsonObject(name, surname, year);
    }

}
