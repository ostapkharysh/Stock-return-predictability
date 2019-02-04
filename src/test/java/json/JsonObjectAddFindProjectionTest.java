package json;

import org.junit.Test;
import org.skyscreamer.jsonassert.JSONAssert;

import static org.junit.Assert.*;

/**
 * Created by Andrii_Rodionov on 1/5/2017.
 */
public class JsonObjectAddFindProjectionTest {
    @Test
    public void testAddToEmptyJsonObject() throws Exception {
        JsonObject jsonObject = new JsonObject();
        jsonObject.add(new JsonPair("attribute", new JsonString("value")));

        String expectedJSON = "{'attribute': 'value'}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }


    @Test
    public void testAddNewPair() throws Exception {
        JsonObject jsonObject = new JsonObject(new JsonPair("name", new JsonString("Oles")));
        jsonObject.add(new JsonPair("age", new JsonNumber(19)));

        String expectedJSON = "{'name': 'Oles', 'age': 19}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }

    @Test
    public void testAddUpdateExistingValue() throws Exception {
        JsonObject jsonObject =
                new JsonObject(
                        new JsonPair("name", new JsonString("Oles")),
                        new JsonPair("age", new JsonNull())
                );
        jsonObject.add(new JsonPair("age", new JsonNumber(19)));

        String expectedJSON = "{'name': 'Oles', 'age': 19}";

        JSONAssert.assertEquals(expectedJSON, jsonObject.toJson(), true);
    }

    @Test
    public void testFindExists() throws Exception {
        JsonObject jsonObject =
                new JsonObject(
                        new JsonPair("name", new JsonString("Oles")),
                        new JsonPair("age", new JsonNumber(23))
                );
        Json json = jsonObject.find("age");

        assertEquals("23", json.toJson());
    }

    @Test
    public void testFindNotExists() throws Exception {
        JsonObject jsonObject =
                new JsonObject(
                        new JsonPair("name", new JsonString("Oles")),
                        new JsonPair("age", new JsonNumber(23))
                );
        Json json = jsonObject.find("surname");

        assertNull(json);
    }


    @Test
    public void testProjectionNoMatches() throws Exception {
        JsonObject jsonObject = new JsonObject(
                new JsonPair("name", new JsonString("Andrii")),
                new JsonPair("year", new JsonNumber(2))
        );

        JsonObject jsonObjectProjection = jsonObject.projection("surname", "age", "marks");

        String expectedJSON = "{}";

        JSONAssert.assertEquals(expectedJSON, jsonObjectProjection.toJson(), true);
    }

    @Test
    public void testProjectionPartialMatches() throws Exception {
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

        JsonObject jsonObjectProjection = jsonObject.projection("surname", "age", "marks", "year");

        String expectedJSON = "{'surname': 'Rodionov', 'year': 2, 'marks': [3, 4, 2]}";

        JSONAssert.assertEquals(expectedJSON, jsonObjectProjection.toJson(), true);
    }

}