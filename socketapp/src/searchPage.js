import React from "react";
import data_table from "./dataTable";
import { Button } from 'react-native';

const search_page = (button_handler, table_data) => {
    return (
        <div>
            <Button title="🔄" onPress={button_handler}> </Button>
            {data_table(table_data)}
        </div>
    )
};



export default search_page;