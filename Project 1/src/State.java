import java.util.ArrayList;
import java.util.LinkedList;

public class State {

    private Graph graph;
    private int selectedNodeId;
    private State parentState;

    public State(Graph graph, int selectedNodeId, State parentState){
        this.graph= graph.copy();
        this.selectedNodeId= selectedNodeId;
        if(parentState != null){
            this.parentState= parentState;
        }else{
            this.parentState = null;
        }
    }

    public ArrayList<State> successor(){
        ArrayList<State> children= new ArrayList<State>();
        for (int i = 0; i < this.graph.size(); i++) {
            int nodeId= this.graph.getNode(i).getId();
            if(nodeId != selectedNodeId){
                State newState = new State(this.graph.copy(), nodeId, this);
                LinkedList<Integer> nodeNeighbors = newState.getGraph().getNode(nodeId).getNeighborsIds();
                for (int j = 0; j < nodeNeighbors.size(); j++) {
                    int neighborId=nodeNeighbors.get(j);
                    newState.getGraph().getNode(neighborId).reverseNodeColor();
                }
                if(newState.getGraph().getNode(nodeId).getColor() == Color.Black){
                    int greenNeighborsCount=0;
                    int redNeighborsCount=0;
                    int blackNeighborcount=0;
                    for (int j = 0; j < nodeNeighbors.size(); j++) {
                        int neighborId=nodeNeighbors.get(j);
                        switch (newState.getGraph().getNode(neighborId).getColor()) {
                            case Green -> greenNeighborsCount++;
                            case Red -> redNeighborsCount++;
                            case Black -> blackNeighborcount++;
                        }
                    }
                    if(greenNeighborsCount > redNeighborsCount && greenNeighborsCount > blackNeighborcount){
                        newState.getGraph().getNode(nodeId).changeColorTo(Color.Green);
                    }else if(redNeighborsCount > greenNeighborsCount && redNeighborsCount > blackNeighborcount){
                        newState.getGraph().getNode(nodeId).changeColorTo(Color.Red);
                    }
                }else {
                    newState.getGraph().getNode(nodeId).reverseNodeColor();
                }
                children.add(newState);
            }
        }
        return children;
    }

    public String hash(){
        String result= "";
        for (int i = 0; i < graph.size(); i++) {
            switch (graph.getNode(i).getColor()) {
                case Green -> result += "g";
                case Red -> result += "r";
                case Black -> result += "b";
            }
        }
        return result;
    }

    public String outputGenerator(){
        String result= "";
        for (int i = 0; i < graph.size(); i++) {
            String color = switch (graph.getNode(i).getColor()) {
                case Red -> "R";
                case Green -> "G";
                case Black -> "B";
            };
            result += graph.getNode(i).getId()+color+" ";
            for (int j = 0; j < graph.getNode(i).getNeighborsIds().size(); j++) {
                int neighborId=graph.getNode(i).getNeighborsId(j);
                String neighborColor = switch (graph.getNode(neighborId).getColor()) {
                    case Red -> "R";
                    case Green -> "G";
                    case Black -> "B";
                };
                result += neighborId+neighborColor+" ";
            }
            result += ",";
        }
        return result;
    }

    public Graph getGraph(){
        return graph;
    }

    public State getParentState(){
        return parentState;
    }

    public  int getSelectedNodeId(){
        return selectedNodeId;
    }
}
