package json;

/**
 * Created by Andrii_Rodionov on 1/4/2017.
 */
public class JsonBoolean extends Json {

    private final Boolean data;
    public JsonBoolean(Boolean bool) {
        this.data = bool;
    }

    @Override
    public String toJson() {
        return data.toString();
    }
}
