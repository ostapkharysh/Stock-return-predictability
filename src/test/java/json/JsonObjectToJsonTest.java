package json;

import org.junit.Test;
import org.skyscreamer.jsonassert.JSONAssert;


/**
 * Created by Andrii_Rodionov on 1/5/2017.
 */
public class JsonObjectToJsonTest {

    @Test
    public void testToJsonWithZeroPairs() throws Exception {
        JsonObject jsonObject = new JsonObject();

        String expectedJSON = "{}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(),true);
    }

    @Test
    public void testToJsonWithOnePair() throws Exception {
        JsonPair jsonPair = new JsonPair("surname", new JsonString("Nik"));
        JsonObject jsonObject = new JsonObject(jsonPair);

        String expectedJSON = "{'surname': 'Nik'}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }

    @Test
    public void testToJsonWithTwoPairs() throws Exception {
        JsonPair jSurname = new JsonPair("surname", new JsonString("Nik"));
        JsonPair jActive = new JsonPair("active", new JsonBoolean(true));
        JsonObject jsonObject = new JsonObject(jSurname, jActive);

        String expectedJSON = "{'surname': 'Nik', 'active': true}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }


    @Test
    public void testToJsonPairsWithSeveralPairs() throws Exception {
        JsonObject jsonObject = new JsonObject(
                new JsonPair("name", new JsonString("Andrii")),
                new JsonPair("surname", new JsonString("Rodionov")),
                new JsonPair("year", new JsonNumber(2)),
                new JsonPair("marks",
                        new JsonArray(
                                new JsonNumber(3), new JsonNumber(4), new JsonNumber(2)
                        )
                )
        );

        String expectedJSON = "{'name': 'Andrii', 'surname': 'Rodionov', 'year': 2, 'marks': [3, 4, 2]}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }

    @Test
    public void testToJsonPairsWithSameNamesButDifferentValues() throws Exception {
        JsonObject jsonObject = new JsonObject(
                new JsonPair("name", new JsonString("Anna")),
                new JsonPair("age", new JsonNumber(18)),
                new JsonPair("status", new JsonNull()),
                new JsonPair("age", new JsonNumber(20))
        );

        String expectedJSON = "{'name': 'Anna', 'age': 20, 'status': null}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }
}