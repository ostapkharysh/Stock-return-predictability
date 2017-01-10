package json;

/**
 * Created by Andrii_Rodionov on 1/3/2017.
 */
public class JsonString extends Json {
    private final String string;

    public JsonString(String string) {
        this.string = string;
    }

    @Override
    public String toJson() {
        return "'" + string + "'";
    }
}
