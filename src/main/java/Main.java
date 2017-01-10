import domain.Student;
import json.JsonObject;
import json.Tuple;

/**
 * Created by Ostap Kharysh on 10.01.2017.
 */
public class Main {
    public static void main(String[] args) {
        Student student = new Student(
                "Andrii",
                "Rodionov",
                3,
                new Tuple<>("OOP", 3),
                new Tuple<>("English", 5),
                new Tuple<>("Math", 2)
        );

        JsonObject jsonObject = student.toJsonObject();
        System.out.println(jsonObject);
    }

}
