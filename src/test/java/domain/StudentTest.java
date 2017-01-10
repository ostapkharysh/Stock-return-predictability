package domain;

import json.Json;
import json.JsonObject;
import json.Tuple;
import org.junit.Test;
import org.skyscreamer.jsonassert.JSONAssert;

import static org.junit.Assert.*;

/**
 * Created by Andrii_Rodionov on 1/6/2017.
 */
public class StudentTest {
    @Test
    public void testToJsonWithEmptyExams() throws Exception {

        Student student = new Student(
                "Andrii",
                "Rodionov",
                3
        );

        JsonObject jsonObject = student.toJsonObject();

        String expectedJSON =
                "{'name': 'Andrii', 'surname': 'Rodionov', 'year': 3, 'exams': []}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }

    @Test
    public void  testToJsonWithSeveralExams() throws Exception {

        Student student = new Student(
                "Andrii",
                "Rodionov",
                3,
                new Tuple<>("OOP", 3),
                new Tuple<>("English", 5),
                new Tuple<>("Math", 2)
        );

        JsonObject jsonObject = student.toJsonObject();

        String expectedJSON =
                "{'name': 'Andrii', 'surname': 'Rodionov', 'year': 3, 'exams': [" +
                        "{'course': 'OOP', 'mark': 3, 'passed': true}," +
                        "{'course': 'English', 'mark': 5, 'passed': true}," +
                        "{'course': 'Math', 'mark': 2, 'passed': false}" +
                        "]}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }

}