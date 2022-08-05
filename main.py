import requests
import pandas as pd
import config
import os
current_dir = os.getcwd()

def main(store_id=196):
    s = requests.Session()
    headers = config.headers
    termid_dict = {'cong_nghe':4,'do_dung':6,'hoa_my_pham':5,'may_mac':7,'tuoi_song':15}
    #store_id = 196
    df_store_data = dict(pd.read_csv(os.path.join(current_dir,f'store_list.csv'))[['id','ten']].values)
    product_data = pd.DataFrame(columns=['unit', 'groups', 'created', 'sku', 'post_id', 'price', 'discount',
        'promotion', 'position', 'date_begin', 'date_end', 'image', 'name',
        'link', 'quantity', 'noteproduct', 'store'])
    for key in termid_dict.keys():
        max_page = 40 #base on demand 40*64
        for i in range(1,max_page,1):
            pay_load = f'request=w_getProductsTaxonomy&termid={termid_dict[key]}&taxonomy=groups&store={store_id}&trang={i}&items=64'
            resp = s.post('https://cooponline.vn/ajax/',data=pay_load,headers=headers)
            df_tmp = pd.DataFrame(resp.json())
            product_data = pd.concat([product_data,df_tmp])
    product_data['store_name'] = product_data['store'].map(df_store_data)
    if config.configs['export_path'] == '': #if null in export part then export in current dir
        product_data.to_csv(os.path.join(current_dir,f'coop_product_data_{store_id}.csv'),encoding='utf-8-sig')
    else:
        product_data.to_csv(os.path.join(config.configs['export_path'],f'coop_product_data_{store_id}.csv'),encoding='utf-8-sig')

if __name__=='__main__':
    main(196)
    
    