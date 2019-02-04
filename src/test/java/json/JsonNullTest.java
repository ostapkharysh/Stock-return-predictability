package json;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by Andrii_Rodionov on 1/5/2017.
 */
public class JsonNullTest {
    @Test
    public void testToJson() {
        JsonNull jsonNull = new JsonNull();
        assertEquals("null", jsonNull.toJson());
    }
}