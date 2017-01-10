package json;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

/**
 * Created by Andrii_Rodionov on 1/3/2017.
 */
public class JsonArray extends Json {

    private final List<Json> jsons;

    public JsonArray(Json... jsons) {
        this.jsons = Arrays.asList(jsons);
    }

    @Override
    public String toJson() {
        return "[" + getJsonArrBody() + "]";
    }

    private String getJsonArrBody() {
        StringBuilder jsonStr = new StringBuilder();
        Iterator<Json> jsonIterator = jsons.iterator();
        while (jsonIterator.hasNext()) {
            Json json = jsonIterator.next();
            jsonStr.append(json.toJson());
            if (jsonIterator.hasNext()) {
                jsonStr.append(", ");
            }
        }
        return jsonStr.toString();
    }
}
