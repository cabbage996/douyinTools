import json

import requests


def get_douyin_id(video_id):
  headers={
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  }
  url='https://www.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'.format(video_id)
  try:
    result=requests.get(url,headers=headers).text
    resp_json=json.loads(result)
    item_list=resp_json['item_list']
    if not item_list:
      return None
    author=item_list[0]['author']
    return author  
  except Exception as e:
    print(e)


if __name__=='__main__':
  video_id='7156540493596298530'#'7155739045794991373'
  author=get_douyin_id(video_id=video_id)
  print(author)
