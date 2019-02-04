package json;

import java.util.ArrayList;
import java.util.Objects;

/**
 * Created by Andrii_Rodionov on 1/3/2017.
 */
public class JsonObject extends Json {

    private int count;
    private final ArrayList<JsonPair> jsPairs = new ArrayList<JsonPair>(); ;

    public JsonObject(JsonPair... jsonPairs) {
        for(JsonPair p: jsonPairs){
            this.add(p);
        }
    }

    @Override
    public String toJson() {
        String out = "";
        int count = 0;
        if(this.jsPairs.isEmpty()){
            return "{}";
        }

        for(JsonPair jp : this.jsPairs){
            if(this.count ==1){
                return "{'" + jp.key + "': " + jp.value.toJson()+ "}" ;
            }
            if(count == 0){
                out += "{'" + jp.key + "': " + jp.value.toJson() ;
                count++;
            }
            else if(count < this.count-1){
                out += ", '" + jp.key + "': " + jp.value.toJson() ;
                count++;
            }
            else{
                out += ", '" + jp.key + "': " + jp.value.toJson() + "}";
            }

        }
        return out;
    }

    public void add(JsonPair jsonPair) {
        boolean state = false;
        for (JsonPair jp : this.jsPairs) {
            if (Objects.equals(jp.key, jsonPair.key)) {
                this.jsPairs.remove(jp);
                JsonPair newJsP = new JsonPair(jp.key, jsonPair.value);
                this.jsPairs.add(newJsP);
                state = true;
                break;
            }
        }
        if(!state){
            this.jsPairs.add(jsonPair);
            this.count++;
        }

    }

    public Json find(String name) {
        for(JsonPair p: this.jsPairs){
            if (p.key.equals(name)){
                return p.value;
            }
        }
        return null;
    }

    public JsonObject projection(String... names) {
        JsonObject obj = new JsonObject();
        for(JsonPair p : this.jsPairs){
            for( String data: names){
                if(p.key.equals(data)){
                    obj.add(p);
                }
            }
        }
        return obj;
    }
    private boolean contains(String name){
        for(JsonPair p: this.jsPairs){
            if (p.key.equals(name)){
                return true;
            }
        }
        return false;
    }


}
