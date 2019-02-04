package domain;

import json.*;

/**
 * Created by Andrii_Rodionov on 1/3/2017.
 */
public class Student extends BasicStudent {

    String name;
    String surname;
    Integer year;
    private final Tuple<String, Integer>[] exams;

    public Student(String name, String surname, Integer year, Tuple<String, Integer>... exams) {
        this.name = name;
        this.surname = surname;
        this.year = year;
        this.exams = exams;
        }


    @Override
    public JsonObject toJsonObject() {
        JsonPair pairName = new JsonPair("name", new JsonString(this.name));
        JsonPair pairSurname = new JsonPair("surname", new JsonString(this.surname));
        JsonPair pairYear = new JsonPair("year", new JsonNumber(this.year));
        JsonObject json1 = new JsonObject();
        json1.add(pairName);
        json1.add(pairSurname);
        json1.add(pairYear);
        JsonObject json2 = new JsonObject();
        for (int i = 0; i<exams.length; i++){
            json2.add(new JsonPair("course", new JsonString(exams[i].getKey())));
            json2.add(new JsonPair("mark", new JsonNumber(exams[i].getValue())));
            json2.add(new JsonPair("passed", new JsonBoolean(exams[i].getValue() > 3)));
        }

        return json1;
    }
}